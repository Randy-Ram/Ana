__author__ = "rram"

from azure.storage.queue import QueueService
from modules.config import storage_acc_name, storage_acc_key


class AzureQueue:
    def __init__(self, queue_name):
        self.queue_service = QueueService(
            account_name=storage_acc_name, account_key=storage_acc_key
        )
        self.queue_name = queue_name

    def exists(self):
        return self.queue_service.exists(self.queue_name)

    def create_queue(self):
        """
        Create a queue in the MS Storage Account

        :param queue_name: Name of queue to create
        :return: None
        """
        try:
            self.queue_service.create_queue(self.queue_name)
        except Exception as e:
            raise e

    def insert(self, message):
        """
        Insert message onto queue

        :param queue_name: Name of queue to insert message on
        :param message: Actual message - can be text/serialized JSON
        :return: None
        """
        try:
            self.queue_service.put_message(self.queue_name, message)
        except Exception as e:
            raise e

    def peek(self, num_messages=None):
        """
        Look at num_messages amount of messages on the queue without removing it.

        :param queue_name: Name of queue
        :param num_messages: Number of messages to look at
        :return: None
        """
        try:
            messages = self.queue_service.peek_messages(
                self.queue_name, num_messages=num_messages
            )
            for message in messages:
                print(message.content)
        except Exception as e:
            raise e

    def dequeue(self, num_messages=None, visibility_timeout=None):
        """
        Read and remove messages from the queue

        :param queue_name: Name of queue
        :param num_messages: Number of messages to read from the queue. Default is 1, max is 32
        :param visibility_timeout: The amount of time a message that is retrieved but not deleted stays invisible
        :return: None
        """
        messages = self.queue_service.get_messages(
            self.queue_name,
            num_messages=num_messages,
            visibility_timeout=visibility_timeout,
        )
        for message in messages:
            print(message.content)
            self.queue_service.delete_message(
                self.queue_name, message.id, message.pop_receipt
            )

    def get_queue_length(self):
        """
        Retrieves the length of the queue

        :param queue_name: Name of queue
        :return: Number of items on the queue
        """
        metadata = self.queue_service.get_queue_metadata(self.queue_name)
        count = metadata.approximate_message_count
        print(count)
        return count

    def delete_queue(self):
        """
        Deletes a queue in the MS Storage Account

        :param queue_name: Name of queue
        :return: None
        """
        self.queue_service.delete_queue(self.queue_name)


if __name__ == "__main__":
    queue_names = ["anaunknownreq", "anaeachreq", "anaerrormsgs"]

    # Test Functions
    for each_queue in queue_names:
        queue = AzureQueue(each_queue)
        if not queue.exists():
            queue.create_queue()
    # insert_to_queue(queue_name, json.dumps(message))
    # peek_in_queue(queue_name)
    # dequeue_message(queue_name)
    # get_queue_length
